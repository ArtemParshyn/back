def add_success(request):
    """
    Контекст-процессор для добавления переменной 'success' в контекст шаблонов.
    """
    return {
        'success': request.user.is_authenticated
    }