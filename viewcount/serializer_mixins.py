class ViewCountSerializerMixin:
    def get_view_count(self, obj) -> int:
        if count := self.context.get("view_count"):
            return count
        return 0
