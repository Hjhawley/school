import subprocess
import re
import graphviz

urls = [
    'wikipedia.org',
    'youtube.com',
    'pcpartpicker.com',
    # ... add more URLs to meet the requirement of at least 20 different URLs
]

# Initialize Graphviz graph
dot = graphviz.Graph('Internet', strict=True)

def get_tracert_hops(url):
    print(f"Running tracert for {url}")
    # Run tracert and wait for it to complete, then capture its output
    tr = subprocess.run(["tracert", "-d", url], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    output = tr.stdout

    lines = output.strip().split('\n')
    hops = []

    for line in lines:
        print(f"Read line: {line}")
        ip_match = re.search(r'\d+\s+ms\s+\d+\s+ms\s+\d+\s+ms\s+(\d+\.\d+\.\d+\.\d+)', line)
        if ip_match:
            hops.append(ip_match.group(1))
        else:
            # Fallback in case the line does not contain an IP address
            hop_match = re.search(r'\d+\s+\d+ ms .*\s([a-zA-Z0-9.-]*)', line)
            if hop_match and not hop_match.group(1).startswith('['):
                hops.append(hop_match.group(1))

    return hops

for url in urls:
    previous_hop = None
    hops = get_tracert_hops(url)
    if not hops:
        print(f"No hops found for {url}. Skipping...")
        continue
    for hop in hops:
        dot.node(hop)
        if previous_hop:
            dot.edge(previous_hop, hop)
        previous_hop = hop
    if previous_hop:
        dot.node(url, label=url)
        dot.edge(previous_hop, url)

dot.render('internet_map', view=True)
