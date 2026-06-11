import { apiPost } from './client'

export interface ExportResult {
  fileId: string
  filename: string
  downloadUrl: string
}

/**
 * Send an export request to the backend.
 * Returns fileId, filename, and downloadUrl for the generated ZIP.
 */
export async function exportImage(request: object): Promise<ExportResult> {
  return apiPost<ExportResult>('/api/export', request)
}
