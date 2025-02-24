// Copyright (c) Manabu TERADA
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
} from '@jupyter-widgets/base';

import { MODULE_NAME, MODULE_VERSION } from './version';

// Import the CSS
import '../css/widget.css';

export class NetVisModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: NetVisModel.model_name,
      _model_module: NetVisModel.model_module,
      _model_module_version: NetVisModel.model_module_version,
      _view_name: NetVisModel.view_name,
      _view_module: NetVisModel.view_module,
      _view_module_version: NetVisModel.view_module_version,
      value: 'Hello World',
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    // Add any extra serializers here
  };

  static model_name = 'NetVisModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'NetVisView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

export class NetVisView extends DOMWidgetView {
  render() {
    this.el.classList.add('custom-widget');

    this.value_changed();
    this.model.on('change:value', this.value_changed, this);
  }

  value_changed() {
    this.el.textContent = this.model.get('value');
  }
}
