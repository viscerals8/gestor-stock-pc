export function filtrarPorTexto<T extends Record<string, any>>(
  items: T[],
  texto: string,
  campos: (keyof T)[]
): T[] {
  const buscado = (texto || '').toLowerCase().trim();
  if (!buscado) return items;

  return items.filter((item) =>
    campos.some((campo) => String(item[campo] ?? '').toLowerCase().includes(buscado))
  );
}
