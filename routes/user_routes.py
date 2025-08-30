from flask import Blueprint, request, jsonify
from models import db, User, Service, SOP
from collections import defaultdict

user_bp = Blueprint("user_bp", __name__)

# ------------------- USER ROUTES -------------------

# Create User
@user_bp.route("/users", methods=["POST"])
def add_user():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password_hash = data.get("password")
    if not username or not email or not password_hash:
        return {"error": "username, email, and password are required"}, 400
    user = User(username=username, email=email, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()
    return {"message": f"User {username} added!"}, 201

# Read all Users
@user_bp.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([{
        "id": u.id,
        "username": u.username,
        "email": u.email,
        "role": u.role
    } for u in users])

# Read single User
@user_bp.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return {"error": "User not found"}, 404
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role
    }

# Update User
@user_bp.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return {"error": "User not found"}, 404
    data = request.get_json()
    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email)
    user.password_hash = data.get("password", user.password_hash)
    user.role = data.get("role", user.role)
    db.session.commit()
    return {"message": f"User {user.username} updated!"}

# Delete User
@user_bp.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return {"error": "User not found"}, 404
    db.session.delete(user)
    db.session.commit()
    return {"message": f"User {user.username} deleted!"}

# ------------------- SERVICE ROUTES -------------------

# Create Service
@user_bp.route("/services", methods=["POST"])
def add_service():
    data = request.get_json()
    name = data.get("name")
    version = data.get("version")
    if not name or not version:
        return {"error": "name and version are required"}, 400
    service = Service(name=name, version=version)
    db.session.add(service)
    db.session.commit()
    return {"message": f"Service {name} added!"}, 201

# Read all Services
@user_bp.route("/services", methods=["GET"])
def get_services():
    services = Service.query.all()
    return jsonify([{
        "id": s.id,
        "name": s.name,
        "version": s.version,
        "created_at": s.created_at
    } for s in services])

# Read single Service
@user_bp.route("/services/<int:id>", methods=["GET"])
def get_service(id):
    service = Service.query.get(id)
    if not service:
        return {"error": "Service not found"}, 404
    return {
        "id": service.id,
        "name": service.name,
        "version": service.version,
        "created_at": service.created_at
    }

# Update Service
@user_bp.route("/services/<int:id>", methods=["PUT"])
def update_service(id):
    service = Service.query.get(id)
    if not service:
        return {"error": "Service not found"}, 404
    data = request.get_json()
    service.name = data.get("name", service.name)
    service.version = data.get("version", service.version)
    db.session.commit()
    return {"message": f"Service {service.name} updated!"}

# Delete Service
@user_bp.route("/services/<int:id>", methods=["DELETE"])
def delete_service(id):
    service = Service.query.get(id)
    if not service:
        return {"error": "Service not found"}, 404
    db.session.delete(service)
    db.session.commit()
    return {"message": f"Service {service.name} deleted!"}

# ------------------- SOP ROUTES -------------------

# Create SOP
@user_bp.route("/sops", methods=["POST"])
def add_sop():
    data = request.get_json()
    service_id = data.get("service_id")
    alert = data.get("alert")
    sop_title = data.get("sop_title")
    sop_description = data.get("sop_description")
    sop_link = data.get("sop_link")
    created_by = data.get("created_by")
    last_modified_by = data.get("last_modified_by")
    if not service_id or not alert or not sop_title:
        return {"error": "service_id, alert, and sop_title are required"}, 400
    sop = SOP(
        service_id=service_id,
        alert=alert,
        sop_title=sop_title,
        sop_description=sop_description,
        sop_link=sop_link,
        created_by=created_by,
        last_modified_by=last_modified_by
    )
    db.session.add(sop)
    db.session.commit()
    return {"message": f"SOP {sop_title} added!"}, 201

# Read all SOPs
@user_bp.route("/sops", methods=["GET"])
def get_sops():
    sops = SOP.query.all()
    return jsonify([{
        "id": s.id,
        "service_id": s.service_id,
        "alert": s.alert,
        "sop_title": s.sop_title,
        "sop_description": s.sop_description,
        "sop_link": s.sop_link,
        "created_by": s.created_by,
        "last_modified_by": s.last_modified_by,
        "created_at": s.created_at,
        "updated_at": s.updated_at
    } for s in sops])

# Read single SOP
@user_bp.route("/sops/<int:id>", methods=["GET"])
def get_sop(id):
    sop = SOP.query.get(id)
    if not sop:
        return {"error": "SOP not found"}, 404
    return {
        "id": sop.id,
        "service_id": sop.service_id,
        "alert": sop.alert,
        "sop_title": sop.sop_title,
        "sop_description": sop.sop_description,
        "sop_link": sop.sop_link,
        "created_by": sop.created_by,
        "last_modified_by": sop.last_modified_by,
        "created_at": sop.created_at,
        "updated_at": sop.updated_at
    }

# Update SOP
@user_bp.route("/sops/<int:id>", methods=["PUT"])
def update_sop(id):
    sop = SOP.query.get(id)
    if not sop:
        return {"error": "SOP not found"}, 404
    data = request.get_json()
    sop.service_id = data.get("service_id", sop.service_id)
    sop.alert = data.get("alert", sop.alert)
    sop.sop_title = data.get("sop_title", sop.sop_title)
    sop.sop_description = data.get("sop_description", sop.sop_description)
    sop.sop_link = data.get("sop_link", sop.sop_link)
    sop.created_by = data.get("created_by", sop.created_by)
    sop.last_modified_by = data.get("last_modified_by", sop.last_modified_by)
    db.session.commit()
    return {"message": f"SOP {sop.sop_title} updated!"}

# Delete SOP
@user_bp.route("/sops/<int:id>", methods=["DELETE"])
def delete_sop(id):
    sop = SOP.query.get(id)
    if not sop:
        return {"error": "SOP not found"}, 404
    db.session.delete(sop)
    db.session.commit()
    return {"message": f"SOP {sop.sop_title} deleted!"}

@user_bp.route("/home", methods=["GET"])
def get_sops_grouped():
    # Fetch all services and sops
    services = Service.query.all()
    sops = SOP.query.all()

    # Build a mapping: { service_id: (service_name, version) }
    service_id_map = {service.id: (service.name, service.version) for service in services}

    # Build grouped structure
    grouped = defaultdict(lambda: defaultdict(list))
    for sop in sops:
        service_info = service_id_map.get(sop.service_id)
        if not service_info:
            continue
        service_name, version = service_info

        # ✅ Use get_user() to fetch full user details
        created_by_user = get_user(sop.created_by) if sop.created_by else None
        last_modified_user = get_user(sop.last_modified_by) if sop.last_modified_by else None

        sop_obj = {
            "id": sop.id,
            "alert_name": sop.alert,
            "sop_title": sop.sop_title,
            "sop_description": sop.sop_description,
            "sop_link": sop.sop_link,
            "created_by": created_by_user.get("username") if created_by_user else "Unknown",
            "last_modified_by": last_modified_user.get("username") if last_modified_user else "Unknown",
            "created_at": sop.created_at.strftime("%Y-%m-%d %H:%M:%S") if sop.created_at else None,
            "updated_at": sop.updated_at.strftime("%Y-%m-%d %H:%M:%S") if sop.updated_at else None,
        }

        grouped[service_name][version].append(sop_obj)

    # Format final result
    result = []
    for service_name, versions in grouped.items():
        versions_list = []
        for version, sops_list in versions.items():
            versions_list.append({
                "version": version,
                "sops": sops_list
            })
        result.append({
            "service": service_name,
            "versions": versions_list
        })

    return jsonify(result)


# Get all SOPs by alert name, including their service version
@user_bp.route("/sops/by_alert/<alert_name>", methods=["GET"])
def get_sops_by_alert(alert_name):
    # Find all SOPs with the given alert name (case-insensitive)
    sops = SOP.query.filter(SOP.alert.ilike(alert_name)).all()
    result = []
    for sop in sops:
        service = Service.query.get(sop.service_id)
        result.append({
            "id": sop.id,
            "sop_title": sop.sop_title,
            "sop_description": sop.sop_description,
            "sop_link": sop.sop_link,
            "alert": sop.alert,
            "created_by": sop.created_by,
            "last_modified_by": sop.last_modified_by,
            "created_at": sop.created_at,
            "updated_at": sop.updated_at,
            "service": {
                "id": service.id if service else None,
                "name": service.name if service else None,
                "version": service.version if service else None
            }
        })
    return jsonify(result)

