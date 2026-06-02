import { defineConfig, type Plugin } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { constants } from 'node:fs'
import fs from 'node:fs/promises'
import type { IncomingMessage, ServerResponse } from 'node:http'
import path from 'node:path'

const runsDir = path.resolve(__dirname, '..', 'runs')

function runsMiddleware(): Plugin {
  return {
    name: 'eval-runs-middleware',
    configureServer(server) {
      server.middlewares.use(
        '/runs',
        async (request: IncomingMessage, response: ServerResponse, next: () => void) => {
          const requestPath = decodeURIComponent((request.url ?? '/').split('?')[0] ?? '/')
          const filePath = path.resolve(runsDir, `.${requestPath}`)
          const insideRunsDir = filePath === runsDir || filePath.startsWith(`${runsDir}${path.sep}`)
          if (!insideRunsDir) {
            response.statusCode = 403
            response.end('Forbidden')
            return
          }

          try {
            await fs.access(filePath, constants.R_OK)
            if (path.extname(filePath) === '.json') {
              response.setHeader('Content-Type', 'application/json')
            }
            response.end(await fs.readFile(filePath))
          } catch {
            next()
          }
        }
      )
    },
  }
}

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss(), runsMiddleware()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    fs: {
      allow: [path.resolve(__dirname), path.resolve(__dirname, '..')],
    },
  },
})
