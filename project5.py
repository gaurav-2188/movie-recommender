import wx
import pandas as pd

df = pd.read_csv("movies.csv").fillna("")

df = df.drop_duplicates(subset=["Movie Name"], keep="first").reset_index(drop=True)

df = df[["Movie Name", "Genre", "IMDb Link"]]

app = wx.App()
frame = wx.Frame(None, title="Simple Movie Search", size=(900, 600))

panel = wx.Panel(frame)
layout = wx.BoxSizer(wx.VERTICAL)

search_row = wx.BoxSizer(wx.HORIZONTAL)

label = wx.StaticText(panel, label="Search:")
search_row.Add(label, 0, wx.ALL | wx.CENTER, 5)

search_box = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
search_row.Add(search_box, 1, wx.ALL | wx.EXPAND, 5)

search_button = wx.Button(panel, label="Search")
search_row.Add(search_button, 0, wx.ALL, 5)

layout.Add(search_row, 0, wx.EXPAND)

table = wx.ListCtrl(panel, style=wx.LC_REPORT)
table.InsertColumn(0, "Movie Name")
table.InsertColumn(1, "Genre")
table.InsertColumn(2, "IMDb Link")

layout.Add(table, 1, wx.ALL | wx.EXPAND, 5)

def show_results(data):
    """Show a pandas DataFrame in the table."""
    table.DeleteAllItems()

    if len(data) == 0:
  
        row = table.InsertItem(0, "No results found")
        table.SetItem(row, 1, "")
        table.SetItem(row, 2, "")

        table.SetColumnWidth(0, 250)
        table.SetColumnWidth(1, 200)
        table.SetColumnWidth(2, 350)
        return

    for i, row in data.iterrows():
        idx = table.InsertItem(table.GetItemCount(), row["Movie Name"])
        table.SetItem(idx, 1, row["Genre"])
        table.SetItem(idx, 2, row["IMDb Link"])


    table.SetColumnWidth(0, wx.LIST_AUTOSIZE)
    table.SetColumnWidth(1, wx.LIST_AUTOSIZE)
    table.SetColumnWidth(2, wx.LIST_AUTOSIZE)


def do_search(event):
    """Search for movies containing the typed text."""
    text = search_box.GetValue().strip().lower()

    if text == "":
        show_results(df.head(50))
    else:
        results = df[df["Movie Name"].str.lower().str.contains(text)]
        show_results(results)


def show_info(event):
    """When a movie is double-clicked, show its IMDb link."""
    row = event.GetIndex()
    name = table.GetItemText(row)
    link = table.GetItemText(row, 2)

    wx.MessageBox(f"Movie: {name}\n\nIMDb Link:\n{link}", "Movie Info")

search_button.Bind(wx.EVT_BUTTON, do_search)
search_box.Bind(wx.EVT_TEXT_ENTER, do_search)
table.Bind(wx.EVT_LIST_ITEM_ACTIVATED, show_info)

show_results(df.head(50))


panel.SetSizer(layout)
frame.Show()
app.MainLoop()