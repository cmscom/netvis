// Mock d3 for Jest tests with actual DOM manipulation
let currentElement = null;

const createD3Selection = (element) => {
  currentElement = element;

  return {
    append: jest.fn((tagName) => {
      const newElement = tagName === 'svg'
        ? document.createElementNS('http://www.w3.org/2000/svg', 'svg')
        : document.createElementNS('http://www.w3.org/2000/svg', tagName);
      currentElement.appendChild(newElement);
      return createD3Selection(newElement);
    }),
    attr: jest.fn(function(name, value) {
      if (currentElement) {
        currentElement.setAttribute(name, value);
      }
      return this;
    }),
    style: jest.fn(function(name, value) {
      if (currentElement) {
        currentElement.style[name] = value;
      }
      return this;
    }),
    selectAll: jest.fn(function(selector) {
      return this;
    }),
    data: jest.fn(function() {
      return this;
    }),
    enter: jest.fn(function() {
      return this;
    }),
    exit: jest.fn(function() {
      return this;
    }),
    remove: jest.fn(function() {
      return this;
    }),
    on: jest.fn(function() {
      return this;
    }),
    call: jest.fn(function() {
      return this;
    }),
    classed: jest.fn(function() {
      return this;
    }),
    text: jest.fn(function() {
      return this;
    }),
    select: jest.fn(function() {
      return this;
    }),
    node: jest.fn(() => currentElement),
  };
};

module.exports = {
  select: jest.fn((selector) => {
    const element = typeof selector === 'string'
      ? document.querySelector(selector)
      : selector;
    return createD3Selection(element);
  }),
  forceSimulation: jest.fn(() => ({
    force: jest.fn().mockReturnThis(),
    on: jest.fn().mockReturnThis(),
    alpha: jest.fn().mockReturnThis(),
    restart: jest.fn().mockReturnThis(),
  })),
  forceLink: jest.fn(() => ({
    id: jest.fn().mockReturnThis(),
  })),
  forceManyBody: jest.fn(),
  forceCenter: jest.fn(),
  drag: jest.fn(() => ({
    on: jest.fn().mockReturnThis(),
  })),
  zoom: jest.fn(() => ({
    scaleExtent: jest.fn().mockReturnThis(),
    translateExtent: jest.fn().mockReturnThis(),
    on: jest.fn().mockReturnThis(),
  })),
};
