// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

// Add any needed widget imports here (or from controls)
// import {} from '@jupyter-widgets/base';

import { createTestModel } from './utils';

import { NetVisModel } from '..';

describe('NetVis', () => {
  describe('NetVisModel', () => {
    it('should be createable', () => {
      const model = createTestModel(NetVisModel);
      expect(model).toBeInstanceOf(NetVisModel);
      expect(model.get('value')).toEqual('Hello World');
    });

    it('should be createable with a value', () => {
      const state = { value: 'Foo Bar!' };
      const model = createTestModel(NetVisModel, state);
      expect(model).toBeInstanceOf(NetVisModel);
      expect(model.get('value')).toEqual('Foo Bar!');
    });
  });
});
