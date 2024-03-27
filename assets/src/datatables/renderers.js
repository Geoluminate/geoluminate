export function renderTemplate ( template ) {
  return function ( data, type, row ) {
    if ( type === 'display' & data !== null ) {
      return template.format({'data': data, "object": row})
    }
    return data;
  };
};

export function choiceRenderer ( choices ) {
  return function ( data, type, row ) {
    if ( type === 'display' ) {
      var c = choices.find((o) => { return o["value"] === data })
      if (c === undefined) {
        return data
      }
      return choices.find((o) => { return o["value"] === data })["label"]
    }
    // Search, order and type can use the original data
    return data;
  };
};

export function renderBoolean ( data, type, row ) {
  return function ( data, type, row ) {
    if ( type === 'display' ) {
      return data === true ?
                '<i class="fas fa-check text-success">✔<span style="display:none">' + data + '</span></i>' :
                '<i class="fas fa-times text-danger">✘<span style="display:none">' + data + '</span></i>';
    }
    // Search, order and type can use the original data
    return data;
  };
};
