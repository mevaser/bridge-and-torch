from contextlib import redirect_stdout
from io import StringIO
from itertools import combinations
import os
import subprocess
import sys
import unittest

import bridge_and_torch as bridge


def independent_minimum(times):
    """Relax every legal edge until no distance improves; independent of the UCS queue."""
    end = (1 << len(times)) - 1
    distances = {(0, 0): 0}
    while True:
        updated = False
        for (mask, side), total in list(distances.items()):
            available = [i for i in range(len(times)) if ((mask >> i) & 1) == side]
            for size in (1, 2):
                for group in combinations(available, size):
                    key = mask ^ sum(1 << i for i in group), 1 - side
                    cost = total + max(times[i] for i in group)
                    if cost < distances.get(key, float("inf")):
                        distances[key] = cost
                        updated = True
        if not updated:
            return distances[(end, 1)]


class RouteTests(unittest.TestCase):
    def test_minimum_and_legal_path(self):
        path = bridge.ucs()
        self.assertEqual(independent_minimum(list(bridge.PEOPLE.values())), 28)
        self.assertEqual(path[-1][3], 28)
        self.assertEqual(path[0], (bridge.ALL, set(), "L", 0))
        self.assertEqual(path[-1][:3], (set(), bridge.ALL, "R"))
        for (l, r, torch, elapsed), (nl, nr, nt, total) in zip(path, path[1:]):
            move = l ^ nl
            self.assertEqual(move, r ^ nr)
            self.assertIn(len(move), (1, 2))
            self.assertTrue(move <= (l if torch == "L" else r))
            self.assertNotEqual(torch, nt)
            self.assertEqual(total - elapsed, max(bridge.PEOPLE[p] for p in move))

    def test_import_and_default_without_site_packages(self):
        output = subprocess.check_output([sys.executable, "-S", "-c", "import bridge_and_torch"])
        self.assertEqual(output, b"")
        command = [sys.executable, "-S", "bridge_and_torch.py"]
        runs = [subprocess.check_output(command, env={**os.environ, "PYTHONHASHSEED": seed})
                for seed in ("1", "37")]
        self.assertEqual(runs[0], runs[1])
        self.assertIn(b"Minimum crossing time: 28 minutes", runs[0])

    def test_depth_searches_do_not_claim_minimum_time(self):
        for algorithm in ("bfs", "iddfs"):
            out = StringIO()
            with redirect_stdout(out):
                bridge.main(["--algorithm", algorithm])
            self.assertIn("Route time:", out.getvalue())
            self.assertNotIn("Minimum crossing time", out.getvalue())
