import { Insets } from './types';

export function createDefaultContentInsets(width: number, height: number): Insets {
  return {
    top: Math.floor(height * 0.18),
    right: Math.floor(width * 0.18),
    bottom: Math.floor(height * 0.18),
    left: Math.floor(width * 0.18)
  };
}
