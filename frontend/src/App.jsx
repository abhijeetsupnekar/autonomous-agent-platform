import { useState } from "react";
import api from "./services/api";

function App() {

  const [history, setHistory] = useState([]);
  const [query, setQuery] = useState("");
  const [plan, setPlan] = useState([]);
  const [toolResults, setToolResults] = useState([]);
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("Ready");

  const handleSend = async () => {

    if (!query.trim()) return;

    try {

      setLoading(true);

      setStatus("Planning...");

      const result = await api.post("/chat", {
        query,
      });

      setStatus("Executing MCP Tools...");

      setPlan(result.data.plan || []);

      setToolResults(result.data.tool_results || []);

      setStatus("Generating Response...");

      setResponse(result.data.response || "");

      setHistory((prev) => [
        query,
        ...prev,
      ]);

      setQuery("");

      setStatus("Ready");

    } catch (error) {

      console.error(error);

      setStatus("Error");

    } finally {

      setLoading(false);

    }
  };
  return (

    <div className="h-screen overflow-hidden bg-gray-900 text-white">

      <header className="h-24 border-b border-gray-700 px-8 flex items-center justify-between">

        <div>

          <h1 className="text-4xl font-bold text-orange-400">
            Autonomous Agent Platform
          </h1>

          <p className="text-gray-400 mt-1">
            Powered by LangGraph & MCP
          </p>

        </div>

        <div className="text-right">

          <p className="text-gray-300">
            Developed as a Learning Project by
          </p>

          <p className="text-orange-400 font-semibold">
            Abhijeet M Supnekar
          </p>

        </div>

      </header>

      <div className="h-[calc(100vh-96px)] flex">

        <aside className="w-80 border-r border-gray-700 p-4 flex flex-col gap-4">

          <div className="bg-gray-800 rounded-xl p-4 flex-1">

            <h2 className="text-orange-400 text-xl font-semibold mb-4">
              MCP Servers
            </h2>

            <div className="space-y-4">

              <div>🟢 Product Server</div>

              <div>🟢 Weather Server</div>

              <div>🟢 Exchange Server</div>

            </div>

          </div>

          <div className="bg-gray-800 rounded-xl p-4 h-36 overflow-y-auto">


            <h2 className="text-orange-400 text-xl font-semibold mb-4">
              Available Tools
            </h2>

            <ul className="space-y-1 text-xs">

              <li>search_products</li>

              <li>get_product_by_name</li>

              <li>list_categories</li>

              <li>add_to_cart</li>

              <li>view_cart</li>

              <li>checkout</li>

              <li>get_weather</li>

              <li>convert_currency</li>

            </ul>

          </div>

          <div className="bg-gray-800 rounded-xl p-4 flex-[1] overflow-y-auto">

            <h2 className="text-orange-400 text-xl font-semibold mb-4">
              Request History
            </h2>

            <div className="space-y-2 max-h-full">

              {history.map((item, index) => (

                <button
                  key={index}
                  onClick={() => setQuery(item)}
                  className="w-full text-left bg-gray-900 rounded-lg p-2 text-sm"
                >
                  {item}
                </button>

              ))}

            </div>

          </div>

        </aside>

        <main className="flex-1 p-4 flex flex-col gap-4">

          <div className="bg-gray-800 rounded-xl p-4">

            <h2 className="text-orange-400 text-xl font-semibold mb-4">
              Query Input
            </h2>

            <div className="flex gap-3">

              <input
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Ask your autonomous agent..."
                className="flex-1 bg-gray-900 border border-gray-700 rounded-lg px-4 py-3 outline-none"
              />

              <button
                onClick={handleSend}
                disabled={loading}
                className="bg-orange-500 hover:bg-orange-600 px-6 rounded-lg font-semibold"
              >
                {loading ? "Running..." : "Send"}
              </button>

            </div>

            <div className="mt-3 text-orange-400 text-sm">
              Status: {status}
            </div>

          </div>

          <div className="flex gap-4 h-64">

            <div className="w-1/3 bg-gray-800 rounded-xl p-4 overflow-y-auto">

              <h2 className="text-orange-400 text-xl font-semibold mb-4">
                Execution Plan
              </h2>

              {plan.length === 0 ? (

                <div className="text-gray-500">
                  Execution plan will appear here
                </div>

              ) : (

                plan.map((step, index) => (

                  <div
                    key={index}
                    className="bg-gray-900 rounded-lg p-3 mb-3"
                  >
                    <div className="text-orange-400 font-bold">
                      Step {index + 1}
                    </div>

                    <div>{step.tool_name}</div>

                  </div>

                ))

              )}

            </div>

            <div className="flex-1 bg-gray-800 rounded-xl p-4 overflow-y-auto">

              <h2 className="text-orange-400 text-xl font-semibold mb-4">
                Tool Results
              </h2>

              {toolResults.length === 0 ? (

                <div className="text-gray-500">
                  Tool execution results will appear here
                </div>

              ) : (

                toolResults.map((item, index) => (

                  <div
                    key={index}
                    className="bg-gray-900 rounded-lg p-3 mb-3 border border-gray-700"
                  >

                    <div className="text-orange-400 font-semibold mb-2">
                      {item.tool_name}
                    </div>

                    <div className="text-sm whitespace-pre-wrap">
                      {item.result}
                    </div>

                  </div>

                ))

              )}

            </div>

          </div>

          <div className="flex-1 bg-gray-800 rounded-xl p-4 overflow-y-auto">

            <h2 className="text-orange-400 text-xl font-semibold mb-4">
              Final Response
            </h2>

            {response ? (

              <div className="text-lg leading-8 whitespace-pre-wrap">
                {response}
              </div>

            ) : (

              <div className="text-gray-500">
                Final response will appear here
              </div>

            )}

          </div>

        </main>

      </div>

    </div>

  );
}

export default App;