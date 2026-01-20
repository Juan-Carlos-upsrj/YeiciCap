
export enum ConnectionStatus {
  CONNECTED = 'CONNECTED',
  DISCONNECTED = 'DISCONNECTED',
  CONNECTING = 'CONNECTING',
  ERROR = 'ERROR'
}

export interface StreamMetrics {
  fps: number;
  latency: number;
  packetsPerSecond: number;
  droppedPackets: number;
}

export interface DestinationNode {
  id: string;
  name: string;
  protocol: 'UDP' | 'TCP' | 'Websocket';
  address: string;
  port: number;
  status: ConnectionStatus;
  activeSkeletons: number;
}

export interface MoCapSkeleton {
  id: string;
  name: string;
  boneCount: number;
  markerCount: number;
  lastUpdate: number;
}
