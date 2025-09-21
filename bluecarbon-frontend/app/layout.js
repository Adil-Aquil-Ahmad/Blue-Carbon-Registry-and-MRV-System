import './globals.css'
import { AuthProvider } from './contexts/AuthContext'
import Navigation from './components/Navigation'
import LayoutWrapper from './components/LayoutWrapper'

export const metadata = {
  title: 'BlueCarbon MRV Dashboard',
  description: 'Blue Carbon Registry & MRV - demo frontend'
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          <LayoutWrapper>
            {children}
          </LayoutWrapper>
        </AuthProvider>
      </body>
    </html>
  )
}
