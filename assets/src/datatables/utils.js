import dt from "datatables.net-bs5"
import { choiceRenderer, renderBoolean, renderTemplate } from "./renderers"



export function getTableConfig(table) {
  const configScriptEl = table.find('script').first();
  return JSON.parse(configScriptEl.text());
}

String.prototype.format = function(params) {
  const names = Object.keys(params);
  const vals = Object.values(params);
  return new Function(...names, `return \`${this}\`;`)(...vals);
}

function getKeys (array) {
  return array.map((o) => { return o["key"] })
 }

export function getRenderedRowValues(obj, arr) {
  // Get the object's property names as an array
  const propNames = Object.keys(obj);

  // Iterate through the property names
  for (let i = 0; i < propNames.length; i++) {
    const propName = propNames[i];

    // Replace the object's property value with the corresponding value from the array
    obj[propName] = arr[i];
  }

  return obj;
}



export function buildColumnDefs (config) {
  var columnDefs = []

  // applies a template to a specific field
  $.each(config.field_templates, function (key, val) {
    columnDefs.push({
      targets: key,
      render: renderTemplate(val)
    })
  })



  const metadata = config.metadata || []

  if (metadata.length === 0) {
    return columnDefs
  }

  // group metadata objects by type
  var metadata_by_type = {}
  metadata.forEach((o) => { metadata_by_type[o["type"]] = metadata_by_type[o["type"]] || []; metadata_by_type[o["type"]].push(o) })

  // build column defs for select fields if there are any
  if (getMetadataByType(metadata, "select")) {
    // we need to add them indidually because each render function takes a different set of choices
    getMetadataByType(metadata, "select").forEach((field) => {
      columnDefs.push({
        targets: field["key"],
        render:  choiceRenderer(field["choices"])
      })
    })
  }

  // applies a template to a specified widget type
  $.each(config.widget_templates, function (key, val) {
    if (!getMetadataByType(metadata, key)) {
      return
    }
    columnDefs.push({
      targets: getKeys(getMetadataByType(metadata, key)),
      render: renderTemplate(val)
    })
  })



  if (getMetadataByType(metadata, "checkbox")) {
    columnDefs.push({
      targets: getKeys(getMetadataByType(metadata, "checkbox")),
      render: renderBoolean()
    })
  }
  if (getMetadataByType(metadata, "datetime")) {
    columnDefs.push({
      targets: getKeys(getMetadataByType(metadata, "datetime")),
      render: dt.render.datetime(config.datetime_format)
      // render: DataTable.render.datetime(null)
    })
  }

  return columnDefs

}

export function getMetadataByType (metadata, type) {
  return metadata.filter((o) => { return o["type"] === type })
}
