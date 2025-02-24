// Copyright (c) Manabu TERADA
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
} from '@jupyter-widgets/base';
import * as d3 from 'd3';

import { MODULE_NAME, MODULE_VERSION } from './version';
import Graph, { Node, Link } from './graph';

// Import the CSS
import '../css/widget.css';

interface JsonData {
  nodes: Node[];
  links: Link[];
}

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
      value: '',
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
    this._svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    this._svg.setAttribute('width', '800');
    this._svg.setAttribute('height', '800');
    this._svg.setAttribute('id', 'sample');
    this.el.appendChild(this._svg);

    const value = this.model.get('value');
    // this.el.textContent = value;
    const json_data: JsonData = JSON.parse(value);
    const svg = d3.select(this._svg);
    Graph(svg, json_data);
  }

  value_changed() {
    this.el.textContent = this.model.get('value');
  }
  private _svg: SVGElement;
}
