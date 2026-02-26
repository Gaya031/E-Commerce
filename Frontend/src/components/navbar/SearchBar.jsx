import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Search } from "lucide-react";
import { Input } from "@/components/ui/input";
import { searchAll } from "../../api/search.api";

export default function SearchBar() {
  const navigate = useNavigate();
  const wrapperRef = useRef(null);

  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState({ products: [], stores: [] });
  const [showResults, setShowResults] = useState(false);

  useEffect(() => {
    const onClickOutside = (event) => {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target)) {
        setShowResults(false);
      }
    };

    document.addEventListener("mousedown", onClickOutside);
    return () => document.removeEventListener("mousedown", onClickOutside);
  }, []);

  useEffect(() => {
    const q = query.trim();
    if (q.length < 2) {
      setResults({ products: [], stores: [] });
      return;
    }

    const id = setTimeout(async () => {
      setLoading(true);
      try {
        const res = await searchAll(q);
        setResults({
          products: Array.isArray(res.data?.products) ? res.data.products : [],
          stores: Array.isArray(res.data?.stores) ? res.data.stores : [],
        });
        setShowResults(true);
      } catch {
        setResults({ products: [], stores: [] });
      } finally {
        setLoading(false);
      }
    }, 300);

    return () => clearTimeout(id);
  }, [query]);

  const submit = (e) => {
    e.preventDefault();
    const q = query.trim();
    if (!q) return;
    setShowResults(false);
    navigate(`/products?q=${encodeURIComponent(q)}`);
  };

  return (
    <div ref={wrapperRef} className="relative w-[400px]">
      <form onSubmit={submit}>
        <Input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onFocus={() => query.trim().length >= 2 && setShowResults(true)}
          placeholder="Search for milk, bakery or stores..."
          className="w-full pr-9"
        />
        <Search className="w-4 h-4 text-gray-500 absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none" />
      </form>

      {showResults && (
        <div className="absolute mt-2 w-full bg-white border rounded-xl shadow-lg z-50 max-h-96 overflow-auto">
          {loading && <p className="px-3 py-2 text-sm text-gray-500">Searching...</p>}

          {!loading && results.products.length === 0 && results.stores.length === 0 && (
            <p className="px-3 py-2 text-sm text-gray-500">No results found.</p>
          )}

          {!loading && results.products.length > 0 && (
            <div className="p-2 border-b">
              <p className="px-2 py-1 text-xs font-semibold text-gray-500 uppercase">Products</p>
              {results.products.slice(0, 5).map((p) => (
                <button
                  key={`p-${p.id}`}
                  type="button"
                  className="w-full text-left px-2 py-2 hover:bg-gray-50 rounded"
                  onClick={() => {
                    setShowResults(false);
                    navigate(`/product/${p.id}`);
                  }}
                >
                  <p className="text-sm font-medium">{p.name}</p>
                  <p className="text-xs text-gray-500">₹{p.price}</p>
                </button>
              ))}
            </div>
          )}

          {!loading && results.stores.length > 0 && (
            <div className="p-2">
              <p className="px-2 py-1 text-xs font-semibold text-gray-500 uppercase">Stores</p>
              {results.stores.slice(0, 5).map((s) => (
                <button
                  key={`s-${s.id}`}
                  type="button"
                  className="w-full text-left px-2 py-2 hover:bg-gray-50 rounded"
                  onClick={() => {
                    setShowResults(false);
                    navigate(`/store/${s.id}`);
                  }}
                >
                  <p className="text-sm font-medium">{s.store_name}</p>
                </button>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
