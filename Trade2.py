{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "bd7e32b2-9dcb-413b-9361-3f4fa0f04c90",
   "metadata": {},
   "outputs": [
    {
     "ename": "ObsoleteAttributeException",
     "evalue": "app.run_server has been replaced by app.run",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mObsoleteAttributeException\u001b[0m                Traceback (most recent call last)",
      "Cell \u001b[1;32mIn[1], line 63\u001b[0m\n\u001b[0;32m     61\u001b[0m in_jupyter \u001b[38;5;241m=\u001b[39m \u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mJPY_PARENT_PID\u001b[39m\u001b[38;5;124m\"\u001b[39m \u001b[38;5;129;01min\u001b[39;00m os\u001b[38;5;241m.\u001b[39menviron \u001b[38;5;129;01mor\u001b[39;00m \u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mipykernel_launcher\u001b[39m\u001b[38;5;124m\"\u001b[39m \u001b[38;5;129;01min\u001b[39;00m os\u001b[38;5;241m.\u001b[39msys\u001b[38;5;241m.\u001b[39margv[\u001b[38;5;241m0\u001b[39m]\n\u001b[0;32m     62\u001b[0m \u001b[38;5;28;01mif\u001b[39;00m in_jupyter:\n\u001b[1;32m---> 63\u001b[0m     \u001b[43mapp\u001b[49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43mrun_server\u001b[49m(debug\u001b[38;5;241m=\u001b[39m\u001b[38;5;28;01mTrue\u001b[39;00m, port\u001b[38;5;241m=\u001b[39m\u001b[38;5;241m8050\u001b[39m)  \u001b[38;5;66;03m# Jupyter用\u001b[39;00m\n\u001b[0;32m     64\u001b[0m \u001b[38;5;28;01melse\u001b[39;00m:\n\u001b[0;32m     65\u001b[0m     port \u001b[38;5;241m=\u001b[39m \u001b[38;5;28mint\u001b[39m(os\u001b[38;5;241m.\u001b[39menviron\u001b[38;5;241m.\u001b[39mget(\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mPORT\u001b[39m\u001b[38;5;124m\"\u001b[39m, \u001b[38;5;241m10000\u001b[39m))\n",
      "File \u001b[1;32m~\\anaconda3\\Lib\\site-packages\\dash\\_obsolete.py:22\u001b[0m, in \u001b[0;36mObsoleteChecker.__getattr__\u001b[1;34m(self, name)\u001b[0m\n\u001b[0;32m     20\u001b[0m \u001b[38;5;28;01mif\u001b[39;00m name \u001b[38;5;129;01min\u001b[39;00m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m_obsolete_attributes:\n\u001b[0;32m     21\u001b[0m     err \u001b[38;5;241m=\u001b[39m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m_obsolete_attributes[name]\n\u001b[1;32m---> 22\u001b[0m     \u001b[38;5;28;01mraise\u001b[39;00m err\u001b[38;5;241m.\u001b[39mexc(err\u001b[38;5;241m.\u001b[39mmessage)\n\u001b[0;32m     23\u001b[0m \u001b[38;5;28;01mreturn\u001b[39;00m \u001b[38;5;28mgetattr\u001b[39m(\u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m\u001b[38;5;18m__dict__\u001b[39m, name)\n",
      "\u001b[1;31mObsoleteAttributeException\u001b[0m: app.run_server has been replaced by app.run"
     ]
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
    "# データ読み込み\n",
    "df = pd.read_csv(\"2024BL.csv\")\n",
    "\n",
    "# Dashアプリ初期化\n",
    "app = dash.Dash(__name__)\n",
    "server = app.server\n",
    "\n",
    "# Layout定義\n",
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
    "# Callback定義\n",
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
    "# 起動部分\n",
    "if __name__ == \"__main__\":\n",
    "    in_jupyter = \"JPY_PARENT_PID\" in os.environ or \"ipykernel_launcher\" in os.sys.argv[0]\n",
    "    if in_jupyter:\n",
    "        app.run_server(debug=True, port=8050)  # Jupyter用\n",
    "    else:\n",
    "        port = int(os.environ.get(\"PORT\", 10000))\n",
    "        app.run(host=\"0.0.0.0\", port=port, debug=False)  # Renderなど外部サーバー用\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
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
