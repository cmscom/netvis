module.exports = {
  automock: false,
  moduleNameMapper: {
    '\\.(css|less|sass|scss)$': 'identity-obj-proxy',
    '\\.(svg|png|jpg|jpeg|gif)$': '<rootDir>/__mocks__/fileMock.js',
    '^d3$': '<rootDir>/__mocks__/d3Mock.js',
    '^@jupyterlab/application$': '<rootDir>/__mocks__/@jupyterlab/application.js',
    '^@jupyterlab/rendermime$': '<rootDir>/__mocks__/@jupyterlab/rendermime.js',
    '^@jupyterlab/rendermime-interfaces$': '<rootDir>/__mocks__/@jupyterlab/rendermime-interfaces.js',
    '^@lumino/widgets$': '<rootDir>/__mocks__/@lumino/widgets.js',
  },
  preset: 'ts-jest/presets/js-with-babel',
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],
  testPathIgnorePatterns: ['/lib/', '/node_modules/', '/venv/'],
  testRegex: '/__tests__/.*\\.(spec|test)\\.ts[x]?$',
  transformIgnorePatterns: [
    '/node_modules/(?!(d3|d3-.*|@jupyter(lab|-widgets)|@jupyter/.*|internmap|delaunator|robust-predicates)/)',
  ],
  testEnvironment: 'jsdom',
  testEnvironmentOptions: {
    customExportConditions: ['node', 'node-addons'],
  },
  transform: {
    '^.+\\.tsx?$': ['ts-jest', { tsconfig: '<rootDir>/tsconfig.json' }],
  },
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
};