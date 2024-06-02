from models import Business

class SearchController:
    # Method to execute a search query against the Business model
    def execute_search(self, query):
        try:
            # Store the query for potential future use
            self.search_query = query
            # Execute the search against the Business model
            self.search_results = Business.query.filter(Business.name.contains(query)).all()
            # Return the search results along with a success status code
            return self.search_results, 200
        except Exception as e:
            # In case of any exceptions, return the error message along with a server error status code
            return {'error': str(e)}, 500

    # Method to display the results of the most recent search
    def display_results(self):
        try:
            # Check if a search has been executed prior to this
            if hasattr(self, 'search_results'):
                # If yes, return the search results along with a success status code
                return self.search_results, 200
            # If no search has been executed, return an error message along with a bad request status code
            return {'message': 'No search executed prior to displaying results.'}, 400
        except Exception as e:
            # In case of any exceptions, return the error message along with a server error status code
            return {'error': str(e)}, 500