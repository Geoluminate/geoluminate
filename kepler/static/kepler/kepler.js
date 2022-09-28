import testData from '/static/kepler/test_dataset.json' assert { type: "json" };


const WARNING_MESSAGE = 'A Mapbox Token is required in order to use Kepler.gl. Please provide a valid token in the Django Kepler admin site.';

const CONFIG = JSON.parse(document.getElementById('keplerConfig').textContent);

const MAPBOX_TOKEN = CONFIG.mapbox_token;

function getTheme() {
  if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches | CONFIG.theme == 'dark') {
      return {}
  } else {
    return {'theme': CONFIG.theme}
  }
}

console.log(getTheme())

/* Validate Mapbox Token */
if ((MAPBOX_TOKEN || '') === '' || MAPBOX_TOKEN === 'PROVIDE_MAPBOX_TOKEN') {
  alert(WARNING_MESSAGE);
}

/** STORE **/
const reducers = (function createReducers(redux, keplerGl) {
  return redux.combineReducers({
    // mount keplerGl reducer
    keplerGl: keplerGl.keplerGlReducer.initialState({
      uiState: {
        readOnly: false,
        currentModal: null,
        locale: CONFIG.lang
      }
    })
  });
}(Redux, KeplerGl));

const middleWares = (function createMiddlewares(keplerGl) {
  return keplerGl.enhanceReduxMiddleware([
    // Add other middlewares here
  ]);
}(KeplerGl));

const enhancers = (function craeteEnhancers(redux, middles) {
  return redux.applyMiddleware(...middles);
}(Redux, middleWares));

const store = (function createStore(redux, enhancers) {
  const initialState = {};

  return redux.createStore(
    reducers,
    initialState,
    redux.compose(enhancers)
  );
}(Redux, enhancers));
/** END STORE **/

/** COMPONENTS **/
var KeplerElement = (function makeKeplerElement(react, keplerGl, mapboxToken) {

  return function App() {
    var rootElm = react.useRef(null);
    var _useState = react.useState({
      width: window.innerWidth,
      height: window.innerHeight
    });
    var windowDimension = _useState[0];
    var setDimension = _useState[1];
    react.useEffect(function sideEffect(){
      function handleResize() {
        setDimension({width: window.innerWidth, height: window.innerHeight});
      };
      window.addEventListener('resize', handleResize);
      return function() {window.removeEventListener('resize', handleResize);};
    }, []);
    return react.createElement(
      'div',
      {style: {position: 'absolute', left: 0, width: '100vw', height: '100vh'}},
      
      react.createElement(keplerGl.KeplerGl, {
        mapboxApiAccessToken: mapboxToken,
        id: "map",
        width: windowDimension.width,
        height: windowDimension.height,
        ...getTheme()
      })
    )
  }
}(React, KeplerGl, MAPBOX_TOKEN));

const app = (function createReactReduxProvider(react, reactRedux, KeplerElement) {
  return react.createElement(
    reactRedux.Provider,
    {store},
    react.createElement(KeplerElement, null)
  )
}(React, ReactRedux, KeplerElement));
/** END COMPONENTS **/

/** Render **/
(function render(react, reactDOM, app) {
  reactDOM.render(app, document.getElementById('app'));
}(React, ReactDOM, app));

// The next script will show how to interact directly with Kepler map store -->


(function customize(keplerGl, store) {


  // fetch()
  //     .then((res) => res.json())
  //     .then((config) => {
  //         })


  const loadedData = keplerGl.KeplerGlSchema.load(
    testData,
    CONFIG.default_config
  );

  store.dispatch(keplerGl.addDataToMap({
    datasets: loadedData.datasets,
    // config: loadedData.config,
    options: {
      centerMap: true
    }
  }));

  // store.dispatch(keplerGl.addDataToMap({
  //   datasets: loadedData.datasets,
  // }));

}(KeplerGl, store))