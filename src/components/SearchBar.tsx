"use client";

interface SearchBarProps {
  query: string;
  onQueryChange: (query: string) => void;
  resultCount: number;
  totalCount: number;
}

export function SearchBar({
  query,
  onQueryChange,
  resultCount,
  totalCount,
}: SearchBarProps) {
  return (
    <div className="window mb-4">
      <div className="title-bar">
        <div className="title-bar-text">Search Icons</div>
      </div>
      <div className="window-body">
        <div className="field-row-stacked">
          <label htmlFor="search">
            Find icons by name, tags, description, or DLL:
          </label>
          <input
            id="search"
            type="text"
            value={query}
            onChange={(e) => onQueryChange(e.target.value)}
            placeholder="e.g. folder, network, computer, shell32..."
            autoFocus
          />
        </div>
        <p className="mt-2 text-sm">
          {query
            ? `Showing ${resultCount} of ${totalCount} icons`
            : `${totalCount} icons available`}
        </p>
      </div>
    </div>
  );
}
