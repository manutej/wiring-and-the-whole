import { HashRouter, Route, Routes } from 'react-router-dom'

import { ScrollProgress } from './components/ScrollProgress'
import { SiteNav } from './components/SiteNav'
import { HubPage } from './pages/HubPage'
import { TalkConceptPage } from './pages/TalkConceptPage'

export default function App() {
  return (
    <HashRouter>
      <ScrollProgress />
      <SiteNav />
      <Routes>
        <Route path="/" element={<HubPage />} />
        <Route path="/talk/:slug" element={<TalkConceptPage />} />
      </Routes>
    </HashRouter>
  )
}
