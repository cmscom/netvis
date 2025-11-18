// Jest setup file for polyfills and global mocks

// Polyfill DragEvent for jsdom
if (typeof global.DragEvent === 'undefined') {
  class DragEvent extends MouseEvent {
    constructor(type, init) {
      super(type, init);
      this.dataTransfer = init?.dataTransfer || null;
    }
  }
  global.DragEvent = DragEvent;
}

// Polyfill other events if needed
if (typeof global.PointerEvent === 'undefined') {
  class PointerEvent extends MouseEvent {
    constructor(type, init) {
      super(type, init);
    }
  }
  global.PointerEvent = PointerEvent;
}
