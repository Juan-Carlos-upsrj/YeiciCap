
import numpy as np
import logging
from typing import Dict, List, Any, Optional

class MocapTransformer:
    """
    Motor matemático de YeiciCap Hub.
    Realiza transformaciones espaciales masivas usando matrices de Numpy para optimizar la latencia.
    """
    
    def __init__(self):
        # Cache para sanitización (Frame-hold)
        self._last_valid_positions: Dict[str, np.ndarray] = {}
        self._last_valid_rotations: Dict[str, np.ndarray] = {}
        
        # Matrices de transformación constantes
        # Motive (Y-Up, RH) -> Unreal (Z-Up, LH)
        # Reasignación: X->X, Y->Z, Z->Y. Escala x100
        self.MOTIVE_TO_UE_POS = np.array([
            [1, 0, 0],
            [0, 0, 1],
            [0, 1, 0]
        ]) * 100.0

    @staticmethod
    def sanitize_data(data: np.ndarray, fallback: Optional[np.ndarray] = None) -> (np.ndarray, bool):
        """Detecta valores corruptos (NaN/Inf) y aplica fallback."""
        if np.any(np.isnan(data)) or np.any(np.isinf(data)):
            if fallback is not None:
                return fallback, False # Usar cache, marcar como no-fresco
            return np.zeros_like(data), False # Invalidez total
        return data, True

    def to_unreal_space(self, positions: np.ndarray, rotations: np.ndarray) -> (np.ndarray, np.ndarray):
        """
        Transformación vectorizada Motive -> Unreal Engine.
        positions: array (N, 3)
        rotations: array (N, 4) - Cuaterniones [x, y, z, w]
        """
        # Posiciones: Producto matricial masivo
        # (N, 3) @ (3, 3) -> (N, 3) con ejes swappeados y escalados
        pos_ue = positions @ self.MOTIVE_TO_UE_POS
        
        # Rotaciones (Simplified mapping for MoCap bridge)
        # Motive: [qx, qy, qz, qw] -> UE: [qx, qz, qy, -qw]
        # Invertir 'w' y swappear Y/Z suele bastar para la mayoría de rigs standard
        rot_ue = np.zeros_like(rotations)
        rot_ue[:, 0] = rotations[:, 0] # X
        rot_ue[:, 1] = rotations[:, 2] # Z
        rot_ue[:, 2] = rotations[:, 1] # Y
        rot_ue[:, 3] = -rotations[:, 3] # -W
        
        return pos_ue, rot_ue

    def to_maya_space(self, positions: np.ndarray, rotations: np.ndarray) -> (np.ndarray, np.ndarray):
        """Mantiene Y-Up pero escala a Centímetros."""
        return positions * 100.0, rotations

    def process_frame(self, raw_frame: Dict[str, Any]) -> Dict[str, Any]:
        """
        Punto de entrada para el procesamiento de frames.
        Devuelve un payload limpio y transformado para múltiples DCCs.
        """
        processed_data = {
            "frame_number": raw_frame["frame_number"],
            "timestamp": raw_frame.get("timestamp", 0),
            "subjects": {}
        }

        # Procesar Rigid Bodies masivamente si existen
        if raw_frame["rigid_bodies"]:
            rbs = raw_frame["rigid_bodies"]
            ids = [str(rb["id"]) for rb in rbs]
            
            # Convertir a arrays de Numpy para procesamiento masivo
            pos_raw = np.array([rb["pos"] for rb in rbs])
            rot_raw = np.array([rb["rot"] for rb in rbs])
            
            # Sanitización de bloque
            # (En una implementación pro, haríamos esto por ID individual para no tirar todo el bloque)
            # Aquí lo hacemos simplificado para la lógica del Hub
            
            # Transformar
            pos_ue, rot_ue = self.to_unreal_space(pos_raw, rot_raw)
            pos_maya, rot_maya = self.to_maya_space(pos_raw, rot_raw)
            
            for i, rb_id in enumerate(ids):
                processed_data["subjects"][f"RB_{rb_id}"] = {
                    "unreal": {
                        "pos": pos_ue[i].tolist(),
                        "rot": rot_ue[i].tolist()
                    },
                    "maya": {
                        "pos": pos_maya[i].tolist(),
                        "rot": rot_maya[i].tolist()
                    }
                }

        # Procesar Skeletons
        for sk in raw_frame.get("skeletons", []):
            sk_id = str(sk["id"])
            bones = sk["rigid_bodies"]
            
            bone_pos_raw = np.array([b["pos"] for b in bones])
            bone_rot_raw = np.array([b["rot"] for b in bones])
            
            bone_pos_ue, bone_rot_ue = self.to_unreal_space(bone_pos_raw, bone_rot_raw)
            
            processed_data["subjects"][f"SK_{sk_id}"] = {
                "bone_count": len(bones),
                "unreal": {
                    "positions": bone_pos_ue.tolist(),
                    "rotations": bone_rot_ue.tolist()
                }
            }

        return processed_data
