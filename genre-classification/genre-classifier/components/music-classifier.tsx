'use client'

import { useState } from 'react'
import { Bar, BarChart, XAxis, YAxis, ResponsiveContainer, Tooltip } from 'recharts'
import { Upload } from 'lucide-react'

import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { ChartContainer } from '@/components/ui/chart'

interface PredictionResult {
  predicted_genre: string
  confidence: number
  all_probabilities: {
    [key: string]: number
  }
}

export default function MusicClassifier() {
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<PredictionResult | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0]
    if (selectedFile) {
      setFile(selectedFile)
      setError(null)
    }
  }

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault()
    if (!file) {
      setError('Please select a file')
      return
    }

    setLoading(true)
    setError(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error('Prediction failed')
      }
      const data: PredictionResult = await response.json()
      setResult(data)
    } catch (err) {
      setError('Failed to get prediction. Please try again.')
    } finally {
      setLoading(false)
    }
  }
  
  const chartData = result
    ? Object.entries(result.all_probabilities).map(([genre, probability]) => ({
        genre,
        probability: probability * 100, // Convert to percentage
      }))
    : []

  return (
    <div className="container mx-auto py-8 max-w-2xl">
      <Card>
        <CardHeader>
          <CardTitle>Music Genre Classifier</CardTitle>
          <CardDescription>Upload an audio file to predict its genre</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="flex items-center justify-center w-full">
              <label
                htmlFor="file-upload"
                className="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed rounded-lg cursor-pointer hover:bg-muted/50"
              >
                <div className="flex flex-col items-center justify-center pt-5 pb-6">
                  <Upload className="h-8 w-8 mb-2 text-muted-foreground" />
                  <p className="mb-2 text-sm text-muted-foreground">
                    {file ? file.name : 'Click or drag to upload audio file'}
                  </p>
                </div>
                <input id="file-upload" type="file" accept="audio/*" className="hidden" onChange={handleFileChange} />
              </label>
            </div>
            <Button type="submit" className="w-full" disabled={!file || loading}>
              {loading ? 'Analyzing...' : 'Predict Genre'}
            </Button>
          </form>

          {error && <div className="text-destructive text-center">{error}</div>}

          {result && (
            <div className="space-y-4">
              <div className="text-center">
                <h3 className="text-lg font-semibold mb-1">Predicted Genre:</h3>
                <p className="text-2xl font-bold capitalize">{result.predicted_genre}</p>
                <p className="text-muted-foreground">
                  Confidence: {(result.confidence * 100).toFixed(1)}%
                </p>
              </div>

              <div className="pt-4">
                <h4 className="text-sm font-semibold mb-4">Genre Probabilities</h4>
                <ChartContainer config={{
                    bar: {
                      label: 'Bar Chart',
                      icon: BarChart,
                      color: 'hsl(var(--primary))',
                    },
                  }} className="w-full aspect-[2/1]">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={chartData}>
                      <XAxis
                        dataKey="genre"
                        tickLine={false}
                        axisLine={false}
                        tickFormatter={(value) => value.split('_').join(' ')}
                      />
                      <YAxis
                        tickLine={false}
                        axisLine={false}
                        tickFormatter={(value) => `${value}%`}
                      />
                      <Tooltip
                        cursor={{ fill: 'hsl(var(--muted)/0.3)' }}
                        contentStyle={{
                          background: 'hsl(var(--card))',
                          border: '1px solid hsl(var(--border))',
                          borderRadius: '6px',
                        }}
                        formatter={(value: number) => [`${value.toFixed(1)}%`, 'Probability']}
                        labelFormatter={(label) => label.split('_').join(' ')}
                      />
                      <Bar
                        dataKey="probability"
                        fill="hsl(var(--primary))"
                        radius={[4, 4, 0, 0]}
                        animationDuration={200}
                        activeBar={{ fill: 'hsl(var(--primary)/.8)' }}
                      />
                    </BarChart>
                  </ResponsiveContainer>
                </ChartContainer>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
