# Diagrama Entidad-Relacion - Korva Nicaragua

Generado: 2026-07-30 12:27

```mermaid
erDiagram

    %% DJANGO AUTH + TAG 
    User {
        id BIGINT AUTO_INCREMENT PK
        username VARCHAR(150)
        email VARCHAR(254)
        password VARCHAR(128)
    }
    Tag {
        id BIGINT AUTO_INCREMENT PK
        name VARCHAR(255)
        slug VARCHAR(255)
    }
    TaggedItem {
        id BIGINT AUTO_INCREMENT PK
        object_id INTEGER UNSIGNED
    }
    TaggedItem }o--|| Tag : "pertenece a"
    TaggedItem }o--|| Post : "etiqueta a"

    %% USERS
    EmailVerificationToken {
        token UUID
        created_at DATETIME
        expires_at DATETIME
    }
    EmailVerificationToken ||--|| User : "user"
    Profile {
        business_name VARCHAR(255)
        logo VARCHAR(500)
        banner VARCHAR(500)
        ruc VARCHAR(255)
        verified BOOLEAN
        city VARCHAR(255)
        sector VARCHAR(255)
        popularity_score INTEGER
        followers_count INTEGER
        associates_count INTEGER
        collaborations_count INTEGER
        bio TEXT
        latitude FLOAT
        longitude FLOAT
        created_at DATETIME
        updated_at DATETIME
    }
    Profile ||--|| KorvaAIConfig : "ai config"
    Profile ||--|| BankAccount : "bank account"
    Profile ||--|| User : "user"
    Profile }o--o{ Message : "read messages"
    Profile }o--o{ Event : "attending events"
    Profile }o--o{ Group : "groups"
    Report {
        reason VARCHAR(255)
        description TEXT
        created_at DATETIME
        resolved BOOLEAN
    }
    Report }o--|| User : "reporter"
    Report }o--|| User : "reported"
    Block {
        created_at DATETIME
    }
    Block }o--|| User : "blocker"
    Block }o--|| User : "blocked"
    %% SOCIAL
    Post {
        title VARCHAR(255)
        content TEXT
        image VARCHAR(500)
        video VARCHAR(500)
        timestamp DATETIME
        updated_at DATETIME
        upvotes INTEGER
        downvotes INTEGER
        moderation_status VARCHAR(255)
        moderation_reason TEXT
    }
    Post }o--o| Profile : "author"
    Post }o--o{ Tag : "tags"
    PostImage {
        image VARCHAR(500)
        uploaded_at DATETIME
    }
    PostImage }o--o| Post : "post"
    Vote {
        vote_type VARCHAR(255)
        created_at DATETIME
        updated_at DATETIME
    }
    Vote }o--o| Profile : "user"
    Vote }o--o| Post : "post"
    Comment {
        content TEXT
        timestamp DATETIME
        updated_at DATETIME
        upvotes INTEGER
        downvotes INTEGER
    }
    Comment }o--o| Post : "post"
    Comment }o--o| Profile : "author"
    Favorite {
        created_at DATETIME
    }
    Favorite }o--o| Profile : "user"
    Favorite }o--o| Post : "post"
    %% MARKETPLACE
    Product {
        name VARCHAR(255)
        description TEXT
        price DECIMAL(10,2)
        currency VARCHAR(255)
        category VARCHAR(255)
        image VARCHAR(500)
        contact_whatsapp VARCHAR(255)
        created_at DATETIME
        updated_at DATETIME
        is_active BOOLEAN
        views_count INTEGER
    }
    Product }o--o| Profile : "user"
    ProductFavorite {
        created_at DATETIME
    }
    ProductFavorite }o--o| Profile : "user"
    ProductFavorite }o--o| Product : "product"
    Review {
        rating INTEGER
        comment TEXT
        created_at DATETIME
    }
    Review }o--o| Profile : "reviewer"
    Review }o--o| Profile : "seller"
    Review }o--o| Product : "product"
    Deal {
        title VARCHAR(255)
        description TEXT
        discount_percent INTEGER UNSIGNED
        original_price DECIMAL(10,2)
        deal_price DECIMAL(10,2)
        starts_at DATETIME
        ends_at DATETIME
        is_active BOOLEAN
        created_at DATETIME
    }
    Deal }o--o| Product : "product"
    Deal }o--o| Profile : "seller"
    BankAccount {
        bank VARCHAR(255)
        account_type VARCHAR(255)
        account_number VARCHAR(255)
        account_holder VARCHAR(255)
        id_number VARCHAR(255)
        phone VARCHAR(255)
        verified BOOLEAN
        created_at DATETIME
        updated_at DATETIME
    }
    BankAccount ||--|| Profile : "seller"
    Transaction {
        amount DECIMAL(10,2)
        currency VARCHAR(255)
        commission_percent DECIMAL(10,2)
        commission_amount DECIMAL(10,2)
        seller_amount DECIMAL(10,2)
        reference VARCHAR(255)
        status VARCHAR(255)
        bank VARCHAR(255)
        payment_date DATETIME
        buyer_notes TEXT
        created_at DATETIME
        updated_at DATETIME
    }
    Transaction }o--o| Product : "product"
    Transaction }o--o| Profile : "buyer"
    Transaction }o--o| Profile : "seller"
    PayoutRequest {
        amount DECIMAL(10,2)
        status VARCHAR(255)
        admin_notes TEXT
        created_at DATETIME
        processed_at DATETIME
    }
    PayoutRequest }o--o| Profile : "seller"
    PayoutRequest }o--o| BankAccount : "bank account"
    %% MESSAGING
    Message {
        content TEXT
        image VARCHAR(500)
        video VARCHAR(500)
        timestamp DATETIME
    }
    Message }o--o| Profile : "sender"
    Message }o--o| Profile : "recipient"
    Message }o--o{ Profile : "read by"
    Conversation {
        created_at DATETIME
        updated_at DATETIME
    }
    Conversation }o--o| Profile : "user1"
    Conversation }o--o| Profile : "user2"
    %% NOTIFICATIONS
    Notification {
        notification_type VARCHAR(255)
        title VARCHAR(255)
        message TEXT
        related_object_id INTEGER UNSIGNED
        related_object_type VARCHAR(255)
        is_read BOOLEAN
        created_at DATETIME
    }
    Notification }o--|| User : "recipient"
    Notification }o--|| User : "sender"
    NotificationPreference {
        email_messages BOOLEAN
        email_likes BOOLEAN
        email_comments BOOLEAN
        email_follows BOOLEAN
        email_product_inquiries BOOLEAN
        email_mentions BOOLEAN
        email_system BOOLEAN
        push_messages BOOLEAN
        push_likes BOOLEAN
        push_comments BOOLEAN
        push_follows BOOLEAN
        push_product_inquiries BOOLEAN
        push_mentions BOOLEAN
        push_system BOOLEAN
        created_at DATETIME
        updated_at DATETIME
    }
    NotificationPreference ||--|| User : "user"
    %% CORE
    KorvaAIConfig {
        user_api_key VARCHAR(255)
        grok_api_key VARCHAR(255)
        uses_personal_key BOOLEAN
        preferred_provider VARCHAR(255)
        seen_ai_tutorial BOOLEAN
        total_tokens_used INTEGER UNSIGNED
        monthly_token_limit INTEGER UNSIGNED
        created_at DATETIME
        updated_at DATETIME
    }
    KorvaAIConfig ||--|| Profile : "user"
    AIConversation {
        title VARCHAR(255)
        created_at DATETIME
        updated_at DATETIME
    }
    AIConversation }o--o| Profile : "user"
    AIMessage {
        role VARCHAR(255)
        content TEXT
        tokens_used INTEGER UNSIGNED
        provider VARCHAR(255)
        timestamp DATETIME
    }
    AIMessage }o--o| AIConversation : "conversation"
    %% EVENTS
    Event {
        title VARCHAR(255)
        description TEXT
        category VARCHAR(255)
        date DATE
        time TIME
        location VARCHAR(255)
        city VARCHAR(255)
        image VARCHAR(500)
        max_attendees INTEGER UNSIGNED
        is_active BOOLEAN
        created_at DATETIME
    }
    Event }o--o| Profile : "organizer"
    Event }o--o{ Profile : "attendees"
    %% GROUPS
    Group {
        name VARCHAR(255)
        description TEXT
        sector VARCHAR(255)
        image VARCHAR(500)
        created_at DATETIME
    }
    Group }o--o| Profile : "admin"
    Group }o--o{ Profile : "members"
    GroupPost {
        content TEXT
        image VARCHAR(500)
        created_at DATETIME
    }
    GroupPost }o--o| Group : "group"
    GroupPost }o--o| Profile : "author"

```