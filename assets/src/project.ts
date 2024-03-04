import './sass/geoluminate.scss'
import './ts/ajax'
import { fetchAPISchema } from "./ts/api"
import './ts/color-theme-switch'
import './ts/custom'
import "./ts/icons"

fetchAPISchema.then((client: any) => {
  client.apis.projects.projects_list({}).then((response: any) => {
    console.log('Response from project_list:', response.body)
  })
})
