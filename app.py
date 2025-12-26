from flask import Flask, render_template, jsonify, request
from grid import PathfindingGrid

app = Flask(__name__)
grid_obj = PathfindingGrid()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/grid')
def get_grid():
    return jsonify({'grid': grid_obj.grid})

@app.route('/api/reset')
def reset():
    grid_obj.reset_visited()
    return jsonify({'status':'ok'})

@app.route('/api/generate-maze')
def generate_maze():
    grid_obj.generate_random_walls()
    return jsonify({'status':'ok'})

@app.route('/api/easter-egg-maze')
def easter_egg_maze():
    grid_obj.generate_easter_egg_maze()
    return jsonify({'status':'ok'})

@app.route('/api/run', methods=['POST'])
def run_algorithm():
    data = request.json
    algorithm = data.get('algorithm', 'astar')
    grid_obj.reset_visited()
    if algorithm=='bfs':
        visited,path,nodes,path_len,time_ms = grid_obj.bfs()
    elif algorithm=='dfs':
        visited,path,nodes,path_len,time_ms = grid_obj.dfs()
    elif algorithm=='astar':
        visited,path,nodes,path_len,time_ms = grid_obj.astar()
    elif algorithm=='iddfs':
        visited,path,nodes,path_len,time_ms = grid_obj.iddfs()
    else:
        return jsonify({'error':'Unknown algorithm'}),400
    return jsonify({
        'visited': visited,
        'path': path,
        'stats': {'nodes_explored':nodes,'path_length':path_len,'time':time_ms}
    })

if __name__=='__main__':
    app.run(debug=True)
