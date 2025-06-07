const supabase = window.supabase.createClient(
  'https://dibljhwqxxsvdwrzhchk.supabase.co',
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRpYmxqaHdxeHhzdmR3cnpoY2hrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDkyMzgwOTAsImV4cCI6MjA2NDgxNDA5MH0.qcbOKHlDjua_ijVa_3mvnfjbZCl1wROJDtZ4naeZZko'
);

document.addEventListener("DOMContentLoaded", async () => {
  const { data: journal, error } = await supabase
    .from('journal')
    .select('*')
    .order('buy_date', { ascending: false });

  if (error) {
    console.error("Error fetching journal:", error);
    return;
  }

  const table = new Tabulator("#journal-table", {
    data: journal,
    layout: "fitColumns",
    columns: [
      { title: "Symbol", field: "symbol", editor: "input" },
      { title: "Buy Date", field: "buy_date", editor: "input" },
      { title: "Buy Price", field: "buy_price", editor: "number" },
      { title: "Quantity", field: "quantity", editor: "number" }
    ],
    cellEdited: async function(cell) {
      const updatedData = cell.getRow().getData();
      await supabase
        .from("journal")
        .update(updatedData)
        .eq("id", updatedData.id);
    }
  });
});
