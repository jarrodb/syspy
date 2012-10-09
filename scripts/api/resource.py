
class Resource(object):
    def __init__(self,con):
        self._con = con
        self._resource = self.__class__.__name__.lower()

    # public:
    def get(self, **kwargs):
        return self._con.get(self._resource, kwargs)

    def create(self, **kwargs):
        return self._con.post(self._resource, kwargs or {})

    def update(self, **kwargs):
        return self._con.put(self._resource, kwargs)

    def delete(self, **kwargs):
        # return self._con.put(self._resource, kwargs)
        pass

    def write_response(self, r_obj):
        if r_obj.status_code == 200:
            return r_obj.json
        else:
            error = r_obj.json.get('error', None) if r_obj.json else 'error'
            return {
                'error': error,
                'status_code': r_obj.status_code,
                }

    # private:
    def _row_dict(self, row):
        d = {}
        for column in row.__table__.columns:
            d[column.name] = getattr(row, column.name)
        return d

