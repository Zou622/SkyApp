def role_user(request):
    est_technicien = False

    if request.user.is_authenticated:
        try:
            # ✅ CORRECTED: Access technicien_profile through employe relationship
            # Original code (commented): est_technicien = request.user.technicien is not None
            
            est_technicien = (
                request.user.employe and 
                hasattr(request.user.employe, 'technicien_profile') and 
                request.user.employe.technicien_profile is not None
            )
        except:
            est_technicien = False

    return {
        'est_technicien': est_technicien
    }