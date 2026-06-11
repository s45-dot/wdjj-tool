export interface UploadResult {
  imageId: string
  filename: string
  width: number
  height: number
  sizeBytes: number
}

/**
 * Upload a PNG image to the backend.
 * Returns parsed response with imageId, dimensions, and file metadata.
 */
export async function uploadImage(file: File): Promise<UploadResult> {
  const formData = new FormData()
  formData.append('file', file)

  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), 10000)

  try {
    const res = await fetch('http://127.0.0.1:8080/api/upload', {
      method: 'POST',
      body: formData,
      signal: controller.signal,
    })
    if (!res.ok) {
      const text = await res.text()
      throw new Error(`Upload failed (${res.status}): ${text}`)
    }
    const data = await res.json()
    return {
      imageId: data.imageId,
      filename: data.filename,
      width: data.width,
      height: data.height,
      sizeBytes: data.sizeBytes,
    }
  } finally {
    clearTimeout(timer)
  }
}
