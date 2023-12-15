from flask import Flask, jsonify, request
from utils.data_handler import read_data, write_data

app = Flask(__name__)
listings_data = read_data('data/airbnb.json')  # Load Airbnb data on app start
next_id = max(listing['id'] for listing in listings_data) + 1 if listings_data else 1  # Determine next ID

@app.route('/listings', methods=['GET'])
def get_all_listings():
    if len(request.args) == 0:
        return jsonify(listings_data), 200
    
    filtered_listings = listings_data[:]

    if 'price_gt' in request.args:
        price_gt = float(request.args.get('price_gt'))
        filtered_listings = [listing for listing in filtered_listings if listing.get('price', 0.0) > price_gt]

    if 'price_lt' in request.args:
        price_lt = float(request.args.get('price_lt'))
        filtered_listings = [listing for listing in filtered_listings if listing.get('price', float('inf')) < price_lt]

    if 'neighborhood' in request.args:
        neighborhood = request.args.get('neighborhood')
        filtered_listings = [listing for listing in filtered_listings if listing.get('neighborhood') == neighborhood]
    return jsonify(filtered_listings), 200

@app.route('/listings/<int:listing_id>', methods=['GET'])
def get_listing_by_id(listing_id):
    listing = next((listing for listing in listings_data if listing['id'] == listing_id), None)
    if listing:
        return jsonify(listing), 200
    return jsonify({'error': 'Listing not found'}), 404

@app.route('/listings', methods=['POST'])
def create_listing():
    global next_id, listings_data

    if not request.json:
        return jsonify({'error': 'Invalid request body'}), 400

    new_listing = request.json
    new_listing['id'] = next_id
    next_id += 1

    listings_data.append(new_listing)
    write_data('data/airbnb.json', listings_data)

    return jsonify({'message': 'Listing created successfully', 'id': new_listing['id']}), 201

@app.route('/listing/search', methods=['POST'])
def search_listings():
    if not request.json or 'search_terms' not in request.json:
        return jsonify({'error': 'Invalid request body'}), 400

    search_terms = request.json['search_terms'].lower()
    matched_listings = [listing for listing in listings_data if search_terms in listing.get('name', '').lower()]

    return jsonify(matched_listings), 200

@app.route('/listings/<int:listing_id>', methods=['PATCH'])
def update_listing(listing_id):
    listing = next((listing for listing in listings_data if listing['id'] == listing_id), None)
    if not listing:
        return jsonify({'error': 'Listing not found'}), 404

    update_data = request.json
    for key, value in update_data.items():
        if key != 'id':
            listing[key] = value

    write_data('data/airbnb.json', listings_data)

    return jsonify({'message': 'Listing updated successfully', 'id': listing_id}), 200

@app.route('/listings/<int:listing_id>', methods=['DELETE'])
def delete_listing(listing_id):
    global listings_data

    initial_count = len(listings_data)
    listings_data = [listing for listing in listings_data if listing['id'] != listing_id]

    if len(listings_data) < initial_count:
        write_data('data/airbnb.json', listings_data)
        return jsonify({'message': 'Listing deleted successfully', 'id': listing_id}), 200
    else:
        return jsonify({'error': 'Listing not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
