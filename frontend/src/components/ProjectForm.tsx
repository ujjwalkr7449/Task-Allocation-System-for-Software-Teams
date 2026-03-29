import { FormEvent, useState } from 'react'

interface ProjectFormProps {
  onCreate: (payload: { name: string; description: string; requirements_text: string }) => Promise<void>
}

export function ProjectForm({ onCreate }: ProjectFormProps) {
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [requirements, setRequirements] = useState('')

  const submit = async (event: FormEvent) => {
    event.preventDefault()
    await onCreate({ name, description, requirements_text: requirements })
    setName('')
    setDescription('')
    setRequirements('')
  }

  return (
    <form className="space-y-3 rounded-xl bg-white p-4 shadow" onSubmit={submit}>
      <h2 className="text-lg font-semibold">Create Project</h2>
      <input
        className="w-full rounded border p-2"
        placeholder="Project name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        required
      />
      <input
        className="w-full rounded border p-2"
        placeholder="Project description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        required
      />
      <textarea
        className="w-full rounded border p-2"
        placeholder="Requirements (one line per feature)"
        value={requirements}
        onChange={(e) => setRequirements(e.target.value)}
        required
      />
      <button className="rounded bg-brand px-4 py-2 text-white">Create</button>
    </form>
  )
}
