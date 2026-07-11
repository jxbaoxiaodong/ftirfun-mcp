import asyncio
import os
import unittest
from unittest.mock import patch

import ftirfun_mcp_server as server


class FTIRFunMCPWrapperTests(unittest.TestCase):
    def setUp(self):
        os.environ[server.API_KEY_ENV] = "test-key"
        self.addCleanup(os.environ.pop, server.API_KEY_ENV, None)

    def test_tool_catalog_matches_hosted_workflow(self):
        names = {tool.name for tool in asyncio.run(server.mcp.list_tools())}
        self.assertEqual(
            names,
            {
                "parse_ftir_spectrum",
                "analyze_ftir_spectrum",
                "submit_ftir_report",
                "get_ftir_report_status",
                "explain_peaks",
                "find_spectra",
                "fetch_result",
            },
        )

    def test_submit_report_proxies_to_account_report_endpoint(self):
        with patch.object(server, "_request_json", return_value={"success": True}) as request_mock:
            result = server.submit_ftir_report(
                file_base64="ZGF0YQ==",
                filename="sample.spc",
                sampling_mode="ATR",
            )

        self.assertTrue(result["success"])
        self.assertEqual(request_mock.call_args.kwargs["path"], "/ftir/reports")
        self.assertEqual(request_mock.call_args.kwargs["json_body"]["sampling_mode"], "ATR")

    def test_report_status_uses_task_endpoint_and_query_options(self):
        with patch.object(server, "_request_json", return_value={"success": True}) as request_mock:
            result = server.get_ftir_report_status(
                task_id="task-1",
                language_code="de",
                include_report=True,
            )

        self.assertTrue(result["success"])
        self.assertEqual(request_mock.call_args.kwargs["path"], "/ftir/reports/task-1")
        self.assertEqual(
            request_mock.call_args.kwargs["params"],
            {"language_code": "de", "include_report": True},
        )


if __name__ == "__main__":
    unittest.main()
