def role_user(request):
    est_technicien = False

    if request.user.is_authenticated:
        try:
<<<<<<< HEAD
            # ✅ CORRECTED: Access technicien_profile through employe relationship
            # Original code (commented): est_technicien = request.user.technicien is not None
            
            est_technicien = (
                request.user.employe and 
                hasattr(request.user.employe, 'technicien_profile') and 
                request.user.employe.technicien_profile is not None
            )
=======
            est_technicien = request.user.technicien is not None
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
        except:
            est_technicien = False

    return {
        'est_technicien': est_technicien
    }