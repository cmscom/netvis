// Mock d3 for Jest tests
module.exports = {
  select: jest.fn(() => ({
    append: jest.fn().mockReturnThis(),
    attr: jest.fn().mockReturnThis(),
    style: jest.fn().mockReturnThis(),
    selectAll: jest.fn().mockReturnThis(),
    data: jest.fn().mockReturnThis(),
    enter: jest.fn().mockReturnThis(),
    exit: jest.fn().mockReturnThis(),
    remove: jest.fn().mockReturnThis(),
    on: jest.fn().mockReturnThis(),
    call: jest.fn().mockReturnThis(),
    classed: jest.fn().mockReturnThis(),
    text: jest.fn().mockReturnThis(),
    select: jest.fn().mockReturnThis(),
    node: jest.fn(() => document.createElementNS('http://www.w3.org/2000/svg', 'svg')),
    querySelector: jest.fn(),
  })),
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
