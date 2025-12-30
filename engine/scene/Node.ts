import { Transform } from "./Transform";

export type NodeId = string;

export interface Node {
  id: NodeId;
  name: string;
  type: string;
  transform: Transform;
  children: Node[];
}

