{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "bd7e32b2-9dcb-413b-9361-3f4fa0f04c90",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "\n",
       "        <iframe\n",
       "            width=\"100%\"\n",
       "            height=\"650\"\n",
       "            src=\"http://127.0.0.1:8050/\"\n",
       "            frameborder=\"0\"\n",
       "            allowfullscreen\n",
       "            \n",
       "        ></iframe>\n",
       "        "
      ],
      "text/plain": [
       "<IPython.lib.display.IFrame at 0x2809af063c0>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "import dash\n",
    "from dash import html, dcc\n",
    "from dash.dependencies import Input, Output\n",
    "import plotly.express as px\n",
    "import pandas as pd\n",
    "import os\n",
    "\n",
    "df = pd.read_csv(\"2024BL.csv\")\n",
    "\n",
    "app = dash.Dash(__name__)\n",
    "app.title = \"貿易統計ダッシュボード\"\n",
    "server = app.server  # for Render\n",
    "\n",
    "app.layout = html.Div([\n",
    "    html.H1(\"ドロップダウンで国を選択\"),\n",
    "    dcc.Dropdown(\n",
    "        id='city-dropdown',\n",
    "        options=[{'label': country, 'value': country} for country in df['国'].unique()],\n",
    "        value='総計'\n",
    "    ),\n",
    "    dcc.Graph(id='bar-graph')\n",
    "])\n",
    "\n",
    "@app.callback(\n",
    "    Output('bar-graph', 'figure'),\n",
    "    [Input('city-dropdown', 'value')]\n",
    ")\n",
    "def update_graph(selected_country):\n",
    "    filtered_df = df[df['国'] == selected_country]\n",
    "    melted_df = filtered_df.melt(id_vars=['国'], value_vars=['輸出', '輸入', '貿易収支'])\n",
    "\n",
    "    fig = px.bar(\n",
    "        melted_df,\n",
    "        x='variable',\n",
    "        y='value',\n",
    "        color='variable',\n",
    "        title=f\"2024年、アメリカ　{selected_country}の輸出入、貿易収支\",\n",
    "        labels={'variable': '2024年輸出入、貿易収支', 'value': '額（百万ドル）'}\n",
    "    )\n",
    "\n",
    "    color_map = {'輸出': 'blue', '輸入': 'green', '貿易収支': 'gray'}\n",
    "    fig.for_each_trace(lambda t: t.update(marker_color=color_map.get(t.name, 'black')))\n",
    "\n",
    "    fig.update_layout(\n",
    "        autosize=True,\n",
    "        margin=dict(l=30, r=30, t=30, b=30),\n",
    "        paper_bgcolor='white',\n",
    "        plot_bgcolor='white'\n",
    "    )\n",
    "\n",
    "    fig.update_xaxes(linecolor='black')\n",
    "    fig.update_yaxes(linecolor='black', zeroline=True, zerolinecolor='gray')\n",
    "\n",
    "    return fig\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    port = int(os.environ.get(\"PORT\", 10000))\n",
    "    app.run(host=\"0.0.0.0\", port=port, debug=False)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "f7bfb9a0-b1cf-48d2-84d4-26235ba6aaae",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
