import type { ReactNode } from 'react'

type Column<T> = {
  header: string
  cell: (row: T) => ReactNode
}

type DataTableProps<T> = {
  columns: Column<T>[]
  data: T[]
  emptyMessage?: string
}

export function DataTable<T>({ columns, data, emptyMessage = 'No rows found.' }: DataTableProps<T>) {
  return (
    <div style={{ border: '1px solid rgba(148,163,184,.18)', borderRadius: 16, overflow: 'hidden', background: 'rgba(15,23,42,.72)' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={col.header} style={{ textAlign: 'left', padding: 14, color: '#8aa0c7', fontSize: 13, borderBottom: '1px solid rgba(148,163,184,.12)' }}>{col.header}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.length === 0 ? (
            <tr>
              <td colSpan={columns.length} style={{ padding: 18, color: '#8aa0c7' }}>{emptyMessage}</td>
            </tr>
          ) : (
            data.map((row, idx) => (
              <tr key={idx}>
                {columns.map((col) => (
                  <td key={col.header} style={{ padding: 14, borderBottom: '1px solid rgba(148,163,184,.08)' }}>{col.cell(row)}</td>
                ))}
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  )
}
