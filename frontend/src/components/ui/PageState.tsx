type PageStateProps = {
  title: string
  description?: string
}

export function PageState({ title, description }: PageStateProps) {
  return (
    <div className="page">
      <h1>{title}</h1>
      {description ? <p>{description}</p> : null}
    </div>
  )
}
