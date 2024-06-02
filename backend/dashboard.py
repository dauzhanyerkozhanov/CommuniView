class Dashboard:
    def __init__(self):
        self.metrics = {
            'users': 0,
            'businesses': 0,
            'reviews': 0
        }
        
    def update_metrics(self, new_metrics):
        self.metrics.update(new_metrics)
        
    def get_metrics(self):
        return self.metrics
