// Nave low-poly en espacio de modelo: +x es la proa, +y arriba, +z ala hacia la cámara.
const V = {
  nose: [1.6, 0, 0], canopy: [0.55, 0.34, 0],
  top: [0.15, 0.3, 0], bottom: [0.2, -0.18, 0], near: [0.2, 0.02, 0.32], far: [0.2, 0.02, -0.32],
  tailTop: [-1, 0.22, 0], tailBottom: [-1, -0.14, 0], tailNear: [-1, 0.02, 0.26], tailFar: [-1, 0.02, -0.26],
  wingRootFrontNear: [0.1, -0.02, 0.3], wingRootBackNear: [-0.85, -0.02, 0.24], wingTipNear: [-1.05, -0.1, 1.3],
  wingRootFrontFar: [0.1, -0.02, -0.3], wingRootBackFar: [-0.85, -0.02, -0.24], wingTipFar: [-1.05, -0.1, -1.3],
  finFront: [-0.45, 0.24, 0], finBack: [-1, 0.22, 0], finTip: [-1.15, 0.75, 0],
};

const face = (material, ...names) => ({ material, points: names.map(name => V[name]) });

export const FACES = [
  face('glass', 'nose', 'canopy', 'near'), face('glass', 'nose', 'far', 'canopy'),
  face('hull', 'canopy', 'top', 'near'), face('hull', 'canopy', 'far', 'top'),
  face('hull', 'nose', 'near', 'bottom'), face('hull', 'nose', 'bottom', 'far'),
  face('hull', 'top', 'tailTop', 'tailNear', 'near'), face('dark', 'near', 'tailNear', 'tailBottom', 'bottom'),
  face('dark', 'bottom', 'tailBottom', 'tailFar', 'far'), face('hull', 'far', 'tailFar', 'tailTop', 'top'),
  face('engine', 'tailTop', 'tailFar', 'tailBottom', 'tailNear'),
  face('wing', 'wingRootFrontNear', 'wingTipNear', 'wingRootBackNear'),
  face('wing', 'wingRootFrontFar', 'wingRootBackFar', 'wingTipFar'),
  face('accent', 'finFront', 'finTip', 'finBack'),
];

export const ENGINE = [-1.02, 0.04, 0];

export const MATERIALS = {
  hull: { color: [190, 218, 240], glow: 0 },
  dark: { color: [78, 108, 142], glow: 0 },
  wing: { color: [120, 156, 190], glow: 0 },
  glass: { color: [110, 242, 255], glow: 0.55 },
  accent: { color: [198, 243, 107], glow: 0.35 },
  engine: { color: [198, 243, 107], glow: 0.9 },
};
