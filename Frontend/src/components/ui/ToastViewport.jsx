import { X } from "lucide-react";
import { useToastStore } from "../../store/toast.store";

const typeClasses = {
  success: "bg-green-600 text-white",
  error: "bg-red-600 text-white",
  warning: "bg-amber-500 text-white",
  info: "bg-gray-900 text-white",
};

export default function ToastViewport() {
  const { toasts, removeToast } = useToastStore();
  if (!toasts.length) return null;

  return (
    <div className="fixed top-4 right-4 z-[100] space-y-2 w-[320px]">
      {toasts.map((toast) => (
        <div
          key={toast.id}
          className={`rounded-lg shadow-lg px-4 py-3 flex items-start justify-between gap-3 ${
            typeClasses[toast.type] || typeClasses.info
          }`}
        >
          <p className="text-sm leading-relaxed">{toast.message}</p>
          <button onClick={() => removeToast(toast.id)} className="opacity-80 hover:opacity-100">
            <X className="w-4 h-4" />
          </button>
        </div>
      ))}
    </div>
  );
}
