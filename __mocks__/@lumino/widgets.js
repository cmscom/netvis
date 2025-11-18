// Mock for @lumino/widgets

class Widget {
  constructor() {
    this.node = document.createElement('div');
    this._classes = new Set();
  }

  addClass(className) {
    this._classes.add(className);
    this.node.classList.add(className);
  }

  removeClass(className) {
    this._classes.delete(className);
    this.node.classList.remove(className);
  }
}

module.exports = {
  Widget,
};
