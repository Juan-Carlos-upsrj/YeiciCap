
import numpy as np

class MoCapTransformer:
    """
    Transforma coordenadas de Motive (Y-up, Right-handed) 
    a Unreal (Z-up, Left-handed) y Maya (Y-up).
    """
    @staticmethod
    def motive_to_unreal(position, rotation_quat):
        # Re-mapping ejes: X->X, Y->Z, Z->Y
        # Ajuste de escala (Meters to Centimeters)
        pos_ue = np.array([position[0], position[2], position[1]]) * 100.0
        
        # Ajuste de Cuaternión (Conversión básica)
        rot_ue = np.array([rotation_quat[0], rotation_quat[2], rotation_quat[1], -rotation_quat[3]])
        
        return pos_ue, rot_ue

    @staticmethod
    def motive_to_maya(position, rotation_quat):
        # Maya usa Y-up nativo, similar a Motive, pero requiere ajuste de escala (cm)
        return np.array(position) * 100.0, rotation_quat
