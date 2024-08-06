import SwaggerClient from 'swagger-client'

const currentSite = window.location.origin;
const version = 'v1';

export const fetchAPISchema = SwaggerClient({
  url: `${currentSite}/api/${version}/schema/`
})

fetchAPISchema.then((client) => {
  client.apis.geoluminate.Samples_list({}).then((response) => {
    console.log('Response from samples:', response.body)
  })
})
