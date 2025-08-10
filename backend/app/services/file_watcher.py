"""
File Watcher simple para procesamiento automático de archivos CSV.
Implementación basada en un hilo de polling (sin watchdog) para reducir complejidad.
Características:
- Polling ligero cada pocos segundos (configurable)
- Detección de nuevos archivos CSV en carpeta raw
- Verifica que el archivo esté "estable" (sin crecer) antes de procesar
- Manejo seguro de múltiples archivos llegando casi simultáneamente
- Evita reprocesar archivos ya procesados
"""
import os
import time
import threading
import logging
from typing import Dict, Set
from pathlib import Path
from app.services.csv_processor import csv_processor

logger = logging.getLogger(__name__)

class SimpleCSVWatcher:
    """Watcher basado en polling para una carpeta de archivos CSV."""

    def __init__(self, watch_folder: str = "uploads/csv/raw", poll_interval: float = 2.0, stable_seconds: float = 3.0):
        self.watch_folder = Path(watch_folder)
        self.poll_interval = poll_interval
        self.stable_seconds = stable_seconds
        self._thread: threading.Thread | None = None
        self._stop_event = threading.Event()
        self._lock = threading.Lock()
        self._seen_files: Dict[str, Dict[str, float]] = {}
        # _seen_files[path] = { 'first_seen': t, 'last_size': size, 'last_mtime': mtime, 'last_stable_since': t }
        self._processed: Set[str] = set()
        self._processing: Set[str] = set()
        self._last_cycle_duration: float | None = None

    def start(self):
        if self.is_running:
            logger.warning("File watcher ya está corriendo")
            return True
        try:
            self.watch_folder.mkdir(parents=True, exist_ok=True)
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._run_loop, name="csv-watcher", daemon=True)
            self._thread.start()
            logger.info(f"🔍 File watcher (simple) iniciado - monitoreando: {self.watch_folder.resolve()}")
            return True
        except Exception as e:
            logger.error(f"❌ No se pudo iniciar el file watcher: {e}")
            return False

    def stop(self):
        if not self.is_running:
            logger.warning("File watcher no está activo")
            return
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=5)
        logger.info("🛑 File watcher detenido")

    @property
    def is_running(self) -> bool:
        return self._thread is not None and self._thread.is_alive() and not self._stop_event.is_set()

    def _run_loop(self):
        while not self._stop_event.is_set():
            cycle_start = time.time()
            try:
                self._scan_once()
            except Exception as e:
                logger.error(f"Error en ciclo de watcher: {e}")
            self._last_cycle_duration = time.time() - cycle_start
            # Espera respetando el tiempo ya consumido
            remaining = self.poll_interval
            for _ in range(int(remaining * 10)):
                if self._stop_event.is_set():
                    break
                time.sleep(0.1)

    def _scan_once(self):
        if not self.watch_folder.exists():
            return
        now = time.time()
        try:
            current_files = [f for f in self.watch_folder.iterdir() if f.is_file() and f.suffix.lower() == '.csv']
        except Exception as e:
            logger.error(f"No se pudo listar archivos en {self.watch_folder}: {e}")
            return

        with self._lock:
            for file_path in current_files:
                path_str = str(file_path)
                if path_str in self._processed or path_str in self._processing:
                    continue
                try:
                    stat = file_path.stat()
                except FileNotFoundError:
                    continue
                size = stat.st_size
                mtime = stat.st_mtime
                entry = self._seen_files.get(path_str)
                if entry is None:
                    # Nuevo archivo
                    self._seen_files[path_str] = {
                        'first_seen': now,
                        'last_size': size,
                        'last_mtime': mtime,
                        'last_stable_since': now
                    }
                    logger.info(f"Archivo CSV detectado: {path_str}")
                    continue
                # Si cambió tamaño o mtime reiniciamos ventana de estabilidad
                if size != entry['last_size'] or mtime != entry['last_mtime']:
                    entry['last_size'] = size
                    entry['last_mtime'] = mtime
                    entry['last_stable_since'] = now
                    continue
                # Verificar si alcanzó estabilidad
                if (now - entry['last_stable_since']) >= self.stable_seconds:
                    self._processing.add(path_str)
                    threading.Thread(target=self._process_file_safe, args=(file_path,), daemon=True).start()
            # Limpiar entradas de archivos desaparecidos
            existing_set = {str(p) for p in current_files}
            to_remove = [p for p in self._seen_files.keys() if p not in existing_set and p not in self._processing]
            for p in to_remove:
                self._seen_files.pop(p, None)

    def _process_file_safe(self, file_path: Path):
        path_str = str(file_path)
        filename = file_path.name
        try:
            logger.info(f"Iniciando procesamiento automático de: {filename}")
            if file_path.exists() and file_path.stat().st_size > 0:
                result = csv_processor.procesar_archivo_especifico(filename)
                if result:
                    logger.info(f"✅ Procesamiento completado exitosamente: {filename}")
                else:
                    logger.warning(f"⚠️ Procesamiento falló para: {filename}")
            else:
                logger.warning(f"⚠️ Archivo no válido o vacío: {filename}")
        except Exception as e:
            logger.error(f"❌ Error procesando archivo {filename}: {e}")
        finally:
            with self._lock:
                self._processing.discard(path_str)
                self._processed.add(path_str)
                self._seen_files.pop(path_str, None)

    def status(self) -> dict:
        with self._lock:
            return {
                'is_running': self.is_running,
                'watch_folder': str(self.watch_folder.resolve()),
                'poll_interval': self.poll_interval,
                'stable_seconds': self.stable_seconds,
                'queue_pending': len(self._seen_files),
                'processing': len(self._processing),
                'processed_count': len(self._processed),
                'last_cycle_duration': self._last_cycle_duration
            }

# Instancia global y funciones de fachada para mantener API previa
_file_watcher = SimpleCSVWatcher()

def start_file_watcher():
    return _file_watcher.start()

def stop_file_watcher():
    return _file_watcher.stop()

def get_file_watcher_status():
    return _file_watcher.status()
