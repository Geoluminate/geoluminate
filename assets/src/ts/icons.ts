import { dom, library } from '@fortawesome/fontawesome-svg-core'
import { faGithub, faLinkedin, faTwitter } from '@fortawesome/free-brands-svg-icons'
import { faStar as faStarRegular } from '@fortawesome/free-regular-svg-icons'
import { faArrowLeftLong, faArrowRightToBracket, faBarsStaggered, faBell, faBook, faBookOpen, faComments, faDatabase, faDoorOpen, faEllipsisV, faEnvelope, faFileCode, faFileContract, faFileZipper, faFlag, faFlask, faFolderOpen, faGears, faHouse, faHouseLock, faInstitution, faLink, faMagnifyingGlassChart, faMapLocationDot, faMapMarkerAlt, faPencil, faPlus, faProjectDiagram, faRightFromBracket, faRightToBracket, faRss, faShare, faSpinner, faUser, faUsers, faFileLines, faSitemap, faGlobe } from '@fortawesome/free-solid-svg-icons'

// Add the imported solid icons to the library
library.add(faProjectDiagram, faFolderOpen, faDatabase, faUser, faInstitution, faMapMarkerAlt, faFlask, faMapLocationDot, faBarsStaggered, faUsers, faBookOpen, faRss, faMagnifyingGlassChart, faComments, faPlus, faRightToBracket, faHouseLock, faArrowRightToBracket, faEnvelope, faBell, faLink, faFileContract, faGears, faBook, faEllipsisV, faFileCode, faFlag, faFileZipper, faSpinner, faShare, faPencil, faRightFromBracket, faDoorOpen, faHouse, faArrowLeftLong, faFileLines, faSitemap, faGlobe )

// Add the imported brand icons to the library
library.add(faGithub, faLinkedin, faTwitter)

// Add the imported regular icons to the library
library.add(faStarRegular)


// Make FontAwesome icons available throughout your project
dom.watch()
