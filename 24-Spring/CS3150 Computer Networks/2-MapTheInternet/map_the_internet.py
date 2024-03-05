import subprocess
import re
import graphviz

# A list of URLs to perform traceroute on
urls = [
    'www.wikipedia.org',
    'www.youtube.com',
    # ... add at least 20 different URLs here
]

# This will store the traceroute paths as a dictionary where each URL is a key
traceroutes = {}

# The regex pattern to match IP addresses in the traceroute output
ip_pattern = re.compile(r"\((\d+\.\d+\.\d+\.\d+)\)")

# Run traceroute for each URL and capture the output
for url in urls:
    print(f"Tracing route to {url}")
    tr = subprocess.Popen(["tracert", "-d", url], stdout=subprocess.PIPE)
    hops = []

    while True:
        line = tr.stdout.readline().decode().strip()
        if not line:
            break  # End of output

        # Extract the IP address from the line
        match = ip_pattern.search(line)
        if match:
            ip = match.group(1)
            hops.append(ip)

    traceroutes[url] = hops
    tr.wait()  # Ensure the subprocess has finished

# Initialize a new Graphviz graph
dot = graphviz.Graph('Internet', strict=True)

# Keep track of all unique hops to avoid adding duplicate nodes
unique_hops = set()

# Add nodes and edges for each traceroute
for url, hops in traceroutes.items():
    previous_hop = None
    for hop in hops:
        # Add the hop as a node if it's not already added
        if hop not in unique_hops:
            dot.node(hop)
            unique_hops.add(hop)

        # Add an edge from the previous hop to the current hop
        if previous_hop is not None:
            dot.edge(previous_hop, hop)
        previous_hop = hop

    # Add an edge from the last hop to the destination URL
    # The URL itself is represented as a node
    if hops:
        dot.node(url, label=url)
        dot.edge(hops[-1], url)

# Render the graph to a PDF
dot.render('traceroute_map', format='pdf', view=True)
